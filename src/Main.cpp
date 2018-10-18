//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// main
//

#include <iostream>
#include <fstream>
#include "NeuralNetwork/Convolution2D.hpp"

template <typename T>
NeuralNetwork::Conv2DMatrix<T> getZerosMatrix(uint32_t width, uint32_t height,
					   uint32_t channel) {
	std::vector<T> zeroChannel(channel, 0.0f);
	std::vector<std::vector<T>> zeroRow(width, zeroChannel);
	return (NeuralNetwork::Conv2DMatrix<T>(height, zeroRow));
}

int main()
{
	std::ifstream file("out.model", std::ios::in);
	NeuralNetwork::Convolution2D<float> layer(file, 2, 5, 3, 1);
	auto input = getZerosMatrix<float>(2, 2, 2);
	input[0][0][0] = 1.0f;
	auto res = layer(input);

	for (const auto &row : res)
		for (const auto &col : row) {
			for (const auto &chan : col)
				std::cout << chan << " ";
			std::cout << std::endl;
		}
	return (0);
}
