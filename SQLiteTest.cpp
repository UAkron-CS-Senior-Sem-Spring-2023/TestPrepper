#include "sqlite/sqlite3.h"
#include <iostream>
#include <string>
int main() {
	char* err;
	sqlite3* db;
	sqlite3_stmt* stmt;
	sqlite3_open("myDB.db", &db);
	int rc = 0;
	rc = sqlite3_exec(db, "CREATE TABLE IF NOT EXISTS ComputerParts (Definition VARCHAR(120), Term VARCHAR(120))", NULL, NULL, &err);
	if (rc != SQLITE_OK) {
		std::cout << "error: " << err << std::endl;
	}
	int stop = 1;
	/*while (stop != 0) {
	std::string Definition, Term;
		std::cout << "What's the definition?\n";
		std::cin.ignore();
		std::getline(std::cin, Definition);
		std::cout << "What's the term?\n";
		std::getline(std::cin, Term);

		std::string query = "insert into ComputerParts VALUES('" + Definition + "', '" + Term + "');";
		rc = sqlite3_exec(db, query.c_str(), NULL, NULL, &err);
		if (rc != SQLITE_OK) {
			std::cout << "insert error: " << err << std::endl;
		}
		std::cout << "Continue? 1.Yes 0.No";
		std::cin >> stop;
	}*/
	sqlite3_prepare_v2(db, "select Definition, Term from ComputerParts", -1, &stmt, 0);
	const unsigned char* definition;
	const unsigned char* term;
	int request = 0, accessor = 0;
	while(request >= accessor && stop != 0) {
		std::cin >> request;
		sqlite3_step(stmt);
	definition = sqlite3_column_text(stmt, 0);
	term = sqlite3_column_text(stmt, 1);
	if (request == accessor) {
		std::cout << definition << " ===== " << term << std::endl << "Quit? 0.Yes 1.No";
		sqlite3_reset(stmt);
		std::cin >> stop;
		accessor = 0;
	}
	++accessor;
	}
}
