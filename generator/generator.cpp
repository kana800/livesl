#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>
#include <chrono>
#include <fstream>

#include "htmltemplate.hpp"

using json = nlohmann::json;

int main(int argc, char* argv[]) {
    std::ifstream f("C:\\DEV\\livesl\\scraper\\meta.json");

    /*generating new html file*/
    std::string filename("C:\\DEV\\livesl\\docs\\index.html");
    std::fstream fileout;

    fileout.open(filename, std::ios_base::out);
    if (!fileout.is_open()) {
        std::cerr << "failed to open " << filename << '\n';
        return -1;
    }


    json data = json::parse(f);

    fileout << htmlheader << std::endl;
    std::string postname;
    for (json::iterator it = data.begin(); it != data.end(); ++it) {
        fileout << "\t<div class='posts'>\n" <<
            "\t<div class='info'>\n";
        fileout << "\t\t<code>" << it.key() << "</code>\n";
        fileout << "\t\t<br>\n\t\t<ol>\n";
        for (json::iterator ip = it.value().begin();
            ip != it.value().end(); ip++) {
            if (ip.key() == "PostId") {
                postname = ip.value();
                continue;
            }
            fileout << "\t\t<li>Detected " << ip.key() << ":" << ip.value() << "</li>" << std::endl;
        }
        fileout << "\t\t</ol>" << std::endl;
        fileout << "\t\t<a href='https://www.instagram.com/p/" << postname << "'>Post Link </a>\n";
        fileout << "\t</div>" << std::endl;
        fileout << "\t</div>" << std::endl;
    }

    fileout << footersection1 << std::endl;
    fileout << "<p>Auto-Generated at <code>" << std::chrono::system_clock::now() << "</code> </p>" << std::endl;
    fileout << "</footer>\n";

    fileout << footersection2 << std::endl;


    return 0;
}