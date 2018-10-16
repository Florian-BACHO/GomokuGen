//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// Linear Layer
//

#pragma once
#include <vector>
#include <functional>
#include <fstream>
#include <random>

namespace NN {
	template <typename T>
	class Linear;
};

template <typename T>
class NN::Linear {
public:
	Linear(uint32_t nbEntry, uint32_t nbOut,
	       std::function<T(T)> activation = [](T x){return x;})
		: _activation(activation) {
		for (auto i = 0u; i < nbOut; i++)
			_weights.push_back(generateRandomVector(nbEntry));
		_bias = generateRandomVector(nbOut);
	}
	Linear(uint32_t nbEntry, uint32_t nbOut, std::ifstream &stream,
	       std::function<T(T)> activation = [](T x){return x;})
		: _activation(activation) {
		for (auto i = 0u; i < nbOut; i++)
			_weights.push_back(getVectorFromStream(stream,
							       nbEntry));
		_bias = getVectorFromStream(stream, nbOut);
	}

	std::vector<T> operator()(const std::vector<T> &entry) {
		std::vector<T> out;
		T tmp;

		for (auto i = 0u; i < _weights.size(); i++) {
			tmp = _bias[i];
			for (auto j = 0u; j < entry.size(); j++)
				tmp += entry[j] * _weights[i][j];
			out.push_back(_activation(tmp));
		}
		return out;
	};

private:
	std::vector<T> generateRandomVector(uint32_t size) {
		std::random_device rd;
		std::mt19937 gen(rd());
		std::uniform_real_distribution<float> dis(-1.0, 1.0);
		std::vector<T> out;

		for (auto i = 0u; i < size; i++)
			out.push_back(dis(gen));
		return out;
	};

	std::vector<T> getVectorFromStream(std::ifstream &stream, uint32_t size) {
		std::vector<T> out;
		T tmp;

		for (auto i = 0u; i < size; i++) {
			stream >> tmp;
			out.push_back(tmp);
		}
		return (out);
	}

private:
	std::vector<std::vector<T>> _weights;
	std::vector<T> _bias;
	std::function<T(T)> _activation;
};
