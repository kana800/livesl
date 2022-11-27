#ifndef HTMLTEMPLATE
#define HTMLTEMPLATE

#include <stdio.h>
#include <stdbool.h>
#include <string>

std::string htmlheader =
"<!DOCTYPE html>\n"
"<html>\n"
"<head>\n"
"\t<title>Live SL</title>\n"
"\t<meta name='author' content='opensrilanka'>\n"
"\t<meta name='description' content='shows live-events from a curated-list of bands'>\n"
"\t<meta name='keywords' content='live-events srilanka'>\n"
"\t<meta name='viewport' content='initial-scale=1'>\n"
"\t<link rel='stylesheet' href='styles.css'>\n"
"</head>\n"
"<body>\n"
"\t<p>\n"
"\t\t<span style='font-size:100px'>&#127911</span>\n"
"\t\t<h2>Live-SL</h2>\n"
"\t<p>\n"
;

std::string footersection1 =
"<hr>\n"
"<footer>\n";

std::string footersection2 = "</body>\n"
"</html>\n";


#endif // !HTMLTEMPLATE
