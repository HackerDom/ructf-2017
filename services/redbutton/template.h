#pragma once

class Template
{
public:
	Template(const char *text, const char *name);
	virtual ~Template();

	char *Fill(const char *firstKey, ...);

	char *name;

private:
	char *text;
	int variableCount;
};

class TemplateStorage
{
public:
	TemplateStorage(const char *path);
	virtual ~TemplateStorage();

	Template *GetTemplate(const char *name);

private:
	Template **templates;
	int templateCount;

	void LoadTemplate(const char *path, const char *name);
};