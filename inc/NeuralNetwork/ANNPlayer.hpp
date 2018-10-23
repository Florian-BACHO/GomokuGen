//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// Artificial Neural Network
//

#pragma once

#include <vector>
#include <utility>
#include <fstream>
#include "NeuralNetwork/Convolution2D.hpp"

namespace NeuralNetwork {
	template <typename T>
	class ANNPlayer;

	using PossibleActions = std::vector<std::pair<uint32_t, uint32_t>>;
};

template <typename T>
class NeuralNetwork::ANNPlayer {
public:
	ANNPlayer(const std::string &modelFile)
		: _file(modelFile, std::ios::in),
		  _layer1(file, 2, 4, 5, 2, [this](float x) {return selu(x);}),
		  _layer2(file, 4, 4, 5, 2, [this](float x) {return selu(x);}),
		  _layer3(file, 4, 8, 3, 1, [this](float x) {return selu(x);}),
		  _layer4(file, 8, 8, 3, 1, [this](float x) {return selu(x);}),
		  _out(file, 8, 1, 1, 0, [this](float x) {return selu(x);}),
		{
			_file.close();
		};

	std::pair<uint32_t, uint32_t> operator()
	(const NeuralNetwork::Conv2DMatrix<T> &input,
	 const NeuralNetwork::PossibleActions &possibleActions) const noexcept {
		auto res = _layer1(input);

		res = _layer2(res);
		res = _layer3(res);
		res = _layer4(res);
		res = _out(res);
		return (argmax(res, possibleActions));
	}

private:
	inline T elu(T x, U alpha=1.67326) const noexcept {
		return (x < T() ? (alpha * (std::exp(x) - 1)) : x);
	}

	inline T selu(T x, T scale=1.0507, T alpha=1.67326) const noexcept {
		return scale * elu(x, alpha);
	}

	std::pair<uint32_t, uint32_t> argmax
	(const NeuralNetwork::Conv2DMatrix<T> &output,
	 cosnt NeuralNetwork::PossibleActions &possibleActions) const noexcept {
		auto height = output.size();
		auto width = output[0].size();
		uint32_t x = 0u;
		uint32_t y = 0u;
		T max = output[y][x][0];

		for (auto j = 0u; j < height; j++)
			for (auto i = 0u; i < width; i++)
				if (output[j][i][0] > max &&
				    isPossibleAction(std::make_pair(i, j),
						     possibleActions)) {
					max = output[j][i][0];
					x = i;
					y = j;
				}
		return (std::make_pair(x, y));
	}

	inline bool isPossibleAction(std::pair<uint32_t, uint32_t> action,
				     const NeuralNetwork::PossibleActions
				     &possibleActions) const noexcept {
		return (std::find(possibleActions.begin(),
				  possibleActions.end(),
				  action) != possibleActions.end());
	}

private:
	std::ifstream _file;

	NeuralNetwork::Convolution2D<T> _layer1;
	NeuralNetwork::Convolution2D<T> _layer2;
	NeuralNetwork::Convolution2D<T> _layer3;
	NeuralNetwork::Convolution2D<T> _layer4;
	NeuralNetwork::Convolution2D<T> _out;
};
