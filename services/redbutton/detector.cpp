#include "detector.h"

#include <stdlib.h>
#include <string.h>

Detector::Detector(uuid name, const char *data, size_t length, Detector *previousDetector)
{
	this->data = new char[length];

	memcpy(this->data, data, length);

	this->name = name;
	this->previousDetector = previousDetector;
}

Detector::~Detector()
{
	if (data)
	{
		delete[] data;
		data = NULL;
	}
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

void DetectorStorage::AddDetector(uuid name, const char *data, size_t length)
{
	pthread_mutex_lock(&sync);

	DetectorHeader header;

	header.length = length;
	header.name = name;

	fwrite(&header, sizeof(header), 1, backingFile);
	fwrite(data, 1, length, backingFile);
	fflush(backingFile);

	AddDetectorInternal(name, data, length);

	pthread_mutex_unlock(&sync);
}

void DetectorStorage::AddDetectorInternal(uuid name, const char *data, size_t length)
{
	detectors = new Detector(name, data, length, detectors);
	detectorCount++;
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