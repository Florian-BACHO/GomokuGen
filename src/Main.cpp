//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// main
//

#include <iostream>
#include <fstream>
#include <cmath>
#include "NeuralNetwork/Convolution2D.hpp"

template <typename T>
inline T elu(T x, T alpha=1.67326)
{
	return (x < T() ? (alpha * (std::exp(x) - 1)) : x);
}

template <typename T>
inline T selu(T x, T scale=1.0507, T alpha=1.67326)
{
	return scale * elu(x, alpha);
}

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
	NeuralNetwork::Convolution2D<float> layer1(file, 2, 4, 5, 2, [](float x){return selu(x);});
	NeuralNetwork::Convolution2D<float> layer2(file, 4, 4, 5, 2, [](float x){return selu(x);});
	NeuralNetwork::Convolution2D<float> layer3(file, 4, 8, 3, 1, [](float x){return selu(x);});
	NeuralNetwork::Convolution2D<float> layer4(file, 8, 8, 3, 1, [](float x){return selu(x);});
	NeuralNetwork::Convolution2D<float> out(file, 8, 1, 1, 0, [](float x){return selu(x);});

	auto input = getZerosMatrix<float>(20, 20, 2);
	auto res = layer1(input);
	res = layer2(res);
	res = layer3(res);
	res = layer4(res);
	res = out(res);

	std::cout << selu(-1.0f) << std::endl;
	for (const auto &row : res) {
		for (const auto &col : row)
			for (const auto &chan : col)
				std::cout << chan << " ";
		std::cout << std::endl;
	}
	return (0);
}
