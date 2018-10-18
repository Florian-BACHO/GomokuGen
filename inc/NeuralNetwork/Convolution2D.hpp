//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// Convolution2D
//

#pragma once

#include <fstream>
#include <vector>
#include <functional>

namespace NeuralNetwork {
	template <typename T>
	class Convolution2D;

	// Height, Width, Channels
	template <typename T>
	using Conv2DMatrix = std::vector<std::vector<std::vector<T>>>;
};

template <typename T>
class NeuralNetwork::Convolution2D {
public:
	Convolution2D(std::ifstream &stream, uint32_t inChannel,
		      uint32_t nbFilter, uint32_t kernelSize, uint32_t padding=0,
		      std::function<T(T)> activation = [](T x){return x;})
		: _inChannel(inChannel), _nbFilter(nbFilter),
		  _kernelSize(kernelSize), _padding(padding),
		  _activation(activation) {
		T tmp = T();

		loadKernel(stream);
		for (auto b = 0u; b < nbFilter; b++) {
			stream >> tmp;
			_bias.push_back(tmp);
		}
	}

	Conv2DMatrix<T> operator()(Conv2DMatrix<T> input) const noexcept {
		addPadding(input);
		auto height = input.size();
		auto width = input[0].size();
		Conv2DMatrix<T> out;
		std::vector<std::vector<T>> row;
		std::vector<T> chan;

		for (auto y = 0u; y <= height - _kernelSize; y++) {
			row.clear();
			for (auto x = 0u; x <= width - _kernelSize; x++) {
				chan.clear();
				for (auto f = 0u; f < _nbFilter; f++) {
					chan.push_back(conv(input, x, y, f));
				}
				row.push_back(chan);
			}
			out.push_back(row);
		}
		return (out);
	}

private:
	void loadKernel(std::ifstream &stream)
		noexcept {
		Conv2DMatrix<T> row;
		std::vector<std::vector<T>> col;
		std::vector<T> channel; // composed of filters
		T tmp;

		for (auto y = 0u; y < _kernelSize; y++) {
			row.clear();
			for (auto x = 0u; x < _kernelSize; x++) {
				col.clear();
				for (auto c = 0u; c < _inChannel; c++) {
					channel.clear();
					for (auto f = 0u; f < _nbFilter; f++) {
						stream >> tmp;
						channel.push_back(tmp);
					}
					col.push_back(channel);
				}
				row.push_back(col);
			}
			_kernel.push_back(row);
		}
	}

	void addPadding(Conv2DMatrix<T> &input) const noexcept {
		for (auto i = 0u; i < _padding; i++)
			addZeros(input);
	}

	void addZeros(Conv2DMatrix<T> &input) const noexcept {
		std::vector<T> zerosChannel(_inChannel, T());
		std::vector<std::vector<T>> zerosRow(input[0].size() + 2, zerosChannel);

		for (auto &row : input) {
			row.insert(row.begin(), zerosChannel);
			row.push_back(zerosChannel);
		}
		input.insert(input.begin(), zerosRow);
		input.push_back(zerosRow);
	}

	T conv(const Conv2DMatrix<T> &input, uint32_t x, uint32_t y,
	       uint32_t filterIdx) const noexcept {
		auto out = _bias[filterIdx];

		for (auto y2 = 0u; y2 < _kernelSize; y2++)
			for (auto x2 = 0u; x2 < _kernelSize; x2++)
				for (auto c = 0u; c < _inChannel; c++) {
					out += _kernel[y2][x2][c][filterIdx] *
						input[y + y2][x + x2][c];
				}
		return _activation(out);
	}

private:
	std::vector<Conv2DMatrix<T>> _kernel;
	std::vector<T> _bias;
	uint32_t _inChannel;
	uint32_t _nbFilter;
	uint32_t _kernelSize;
	uint32_t _padding;
	std::function<T(T)> _activation;
};
