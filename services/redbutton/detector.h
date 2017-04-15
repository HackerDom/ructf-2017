#pragma once

#include <stdio.h>
#include <uuid/uuid.h>
#include <stdint.h>
#include <pthread.h>

struct uuid
{
	uuid_t bytes;
};

class Detector
{
public:
	Detector(uuid name, const char *data, size_t length, Detector *previousDetector);
	virtual ~Detector();

	uuid name;
	char *shader;
	size_t shaderSize;
	int targetWidth;
	int targetHeight;

	Detector *previousDetector;
};

struct DetectorHeader
{
	uint32_t length;
	uuid name;
};

class DetectorStorage
{
public:
	DetectorStorage(const char *path);
	virtual ~DetectorStorage();
	
	Detector *GetDetector(uuid name);
	void AddDetector(uuid name, const char *data, size_t length);
	uuid *ListDetectors(int *count);

private:
	Detector *detectors;
	int detectorCount;

	FILE *backingFile;

	pthread_mutex_t sync = PTHREAD_MUTEX_INITIALIZER;

	void AddDetectorInternal(uuid name, const char *data, size_t length);
};