#include "template.h"

#include <string.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

Template::Template(const char *text, const char *name)
{
	this->text = new char[strlen(text) + 1];
	this->name = new char[strlen(name) + 1];

	strcpy(this->text, text);
	strcpy(this->name, name);

	variableCount = 0;

	char *start = this->text;
	while (true)
	{
		start = strstr(start, "{{");

		if (start)
		{
			variableCount++;
			start += 2;
		}
		else
			break;
	}

	printf(":: variable count = %d\n", variableCount);
}

Template::~Template()
{
	if (text)
	{
		delete[] text;
		text = NULL;
	}

	if (name)
	{
		delete[] name;
		name = NULL;
	}
}

char *Template::Fill(const char *firstKey, ...)
{
	va_list args;
	va_start(args, firstKey);

	size_t keyLength = 0;
	size_t valueLength = 0;

	for (int i = 0; i < variableCount * 2; i++)
	{
		const char *arg = i == 0 ? firstKey : va_arg(args, const char *);

		if (i % 2 == 0)
			keyLength += strlen(arg) + 4; // strlen("{{}}")
		else
			valueLength += strlen(arg);
	}

	va_end(args);

	size_t filledLength = strlen(text) + valueLength - keyLength + 1;

	char *filled = new char[filledLength];
	memset(filled, 0, filledLength);

	char *start = text;
	for (int i = 0; i < variableCount; i++)
	{
		char *varStart = strstr(start, "{{");

		strncat(filled, start, varStart - start);

		va_start(args, firstKey);

		for (int j = 0; j < variableCount; j++)
		{
			const char *key = j == 0 ? firstKey : va_arg(args, const char *);
			const char *value = va_arg(args, const char *);

			size_t currentKeyLength = strlen(key);

			printf(":: currentKeyLength = %d\n", currentKeyLength);

			if (!strncmp(key, varStart + 2, currentKeyLength))
			{
				strcat(filled, value);
				start = varStart + currentKeyLength + 4;
				break;
			}
		}

		va_end(args);
	}

	strncat(filled, start, filledLength - strlen(filled) - 1);

	return filled;
}

TemplateStorage::TemplateStorage(const char *path)
{
	DIR *directory = opendir(path);

	if (!directory)
	{
		printf("Failed to open template directory\n");
		exit(1);
	}

	char entries[256][256];
	int count = 0;

	dirent *entry;
	while (entry = readdir(directory))
	{
		if (entry->d_type != DT_REG)
			continue;

		strcpy(entries[count], entry->d_name);

		count++;
	}

	closedir(directory);

	templates = new Template *[count];
	templateCount = 0;

	for (int i = 0; i < count; i++)
	{
		char fileName[256];
		memset(fileName, 0, sizeof(fileName));

		strcat(fileName, path);
		strcat(fileName, "/");
		strcat(fileName, entries[i]);

		LoadTemplate(fileName, entries[i]);
	}
}

TemplateStorage::~TemplateStorage()
{
	if (templates)
	{
		for (int i = 0; i < templateCount; i++)
			delete templates[i];

		delete[] templates;

		templates = NULL;
	}
}

void TemplateStorage::LoadTemplate(const char *path, const char *name)
{
	printf(":: load %s from %s\n", name, path);

	FILE *f = fopen(path, "rb");

	fseek(f, 0, SEEK_END);
	size_t templateSize = ftell(f);
	fseek(f, 0, SEEK_SET);

	char *content = new char[templateSize];

	fread(content, 1, templateSize, f);

	templates[templateCount++] = new Template(content, name);

	delete[] content;

	fclose(f);
}

Template *TemplateStorage::GetTemplate(const char *name)
{
	for (int i = 0; i < templateCount; i++)
	{
		if (!strcmp(name, templates[i]->name))
			return templates[i];
	}

	return NULL;
}