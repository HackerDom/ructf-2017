#include "detector.h"

#include <stdlib.h>
#include <string.h>

Detector::Detector(uuid name, const char *data, size_t length, Detector *previousDetector)
	: shaderSize( 0 ), shader( nullptr ), targetWidth( 0 ), targetHeight( 0 ), previousDetector( nullptr )
{
    // [shader size] [         shader        ] [target width] [target height]
    //     4 bytes    shader size, min 4bytes     4 bytes        4 bytes
	if( length < sizeof( int ) * 4 ) 
		return;

	const int* pShaderSize = ( const int* )data;
	if( *pShaderSize < 4 || *pShaderSize > 8 * 1024 )
		return;

	const int* pWidth = ( const int* )( data + sizeof( int ) + *pShaderSize );
	if( *pWidth <= 0 || *pWidth > 4096 )
		return;

	const int* pHeight = ( const int* )( data + sizeof( int ) + *pShaderSize + sizeof( int ) );
	if( *pHeight <= 0 || *pHeight > 4096 )
		return;

	this->shaderSize = *pShaderSize;
	this->shader = new char[ shaderSize ];
	this->targetWidth = *pWidth;
	this->targetHeight = *pHeight;

	memcpy(this->shader, data + sizeof( int ), this->shaderSize);

	this->name = name;
	this->previousDetector = previousDetector;
}

Detector::~Detector()
{
	delete[] shader;
	shader = NULL;
}


DetectorStorage::DetectorStorage(const char *path)
{
	detectors = NULL;
	detectorCount = 0;

	backingFile = fopen(path, "a+b");

	if (!backingFile)
	{
		printf("Failed to open storage file\n");
		exit(1);
	}

	fseek(backingFile, 0, SEEK_SET);

	DetectorHeader header;
	while (true)
	{
		if (fread(&header, sizeof(header), 1, backingFile) != 1)
			break;

		char *detectorData = new char[header.length];

		fread(detectorData, 1, header.length, backingFile);

		AddDetectorInternal(header.name, detectorData, header.length);

		delete[] detectorData;
	}
}

DetectorStorage::~DetectorStorage()
{
	for (Detector *d = detectors; d != NULL; )
	{
		Detector *prev = d->previousDetector;

		delete d;

		d = prev;
	}

	fclose(backingFile);
}

bool DetectorStorage::AddDetector(uuid name, const char *data, size_t length)
{
	pthread_mutex_lock(&sync);

	bool ret = AddDetectorInternal(name, data, length);
	if( ret ){
		DetectorHeader header;

		header.length = length;
		header.name = name;

		fwrite(&header, sizeof(header), 1, backingFile);
		fwrite(data, 1, length, backingFile);
		fflush(backingFile);
	}

	pthread_mutex_unlock(&sync);

	return ret;
}

bool DetectorStorage::AddDetectorInternal(uuid name, const char *data, size_t length)
{
	Detector* d = new Detector(name, data, length, detectors);
	if( d->shader == nullptr ){
		delete d;
		return false;
	}

	detectors = d;
	detectorCount++;

	return true;
}

uuid *DetectorStorage::ListDetectors(int *count)
{
	*count = detectorCount;

	uuid *list = new uuid[*count];

	int i = 0;
	for (Detector *d = detectors; d != NULL; d = d->previousDetector)
	{
		if (i >= *count)
			break;

		list[i++] = d->name;
	}

	return list;
}

Detector *DetectorStorage::GetDetector(uuid name)
{
	for (Detector *d = detectors; d != NULL; d = d->previousDetector)
	{
		if (!memcmp(&name, &d->name, sizeof(name)))
			return d;
	}

	return NULL;
}