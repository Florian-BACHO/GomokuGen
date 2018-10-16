//
// EPITECH PROJECT, 2018
// Gomoky
// File description:
// Main
//

#include <iostream>
#include "NeuralNetwork/Linear.hpp"

int main()
{
	std::ifstream file("test.dl");
	NN::Linear<float> layer(2, 2, file);
	file.close();
	std::vector<float> entry = {1.0, 1.0};
	auto out = layer(entry);

	for (const auto &it : out)
		std::cout << it << " " << std::endl;
}
