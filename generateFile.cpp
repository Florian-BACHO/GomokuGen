#include <fstream>
#include <iostream>

int main()
{
	std::ofstream file("test.dl", std::ios::out);

	for (auto i = 0u; i < 6; i++)
		file << 0.0f << std::endl;
	return (0);
}
