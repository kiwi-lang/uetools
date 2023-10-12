// {{cookiecutter.copyright}}

#include "{{cookiecutter.plugin_namespace}}Library.h"



void U{{cookiecutter.plugin_name}}Library::GetVersionInfo(FString& GitCommitHash, FString& GitTag, FString& Date)  {
    #define GKSTR_1(x) #x
    #define GKSTR(x) GKSTR_1(x)

        // git rev-parse --no-optional-locks HEAD
        GitCommitHash = GKSTR({{cookiecutter.plugin_upper}}_COMMIT);

        // git describe --no-optional-locks  --tags --abbrev=0
        GitTag = GKSTR({{cookiecutter.plugin_upper}}_TAG);

        // git show --no-optional-locks -s --format=%ci " + Commit
        Date = GKSTR({{cookiecutter.plugin_upper}}_DATE); 

    #undef GKSTR
    #undef GKSTR_1
    }
