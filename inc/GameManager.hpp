//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// Game Manager
//

#pragma once

#include <iostream>
#include <vector>
#include <cstdlib>
#include <Windows.h>
#include "NeuralNetwork/ANNPlayer.hpp"
#include "AGameCommunication.hpp"

namespace Gomoku {
	class GameManager;

	using Board = std::vector<std::vector<std::vector<float>>>;
};

class Gomoku::GameManager : Gomoku::AGameCommunication {
public:
	GameManager()
		: AGameCommunication(), _player("ann.model") {}

	void launchGame() {
		while (true)
			(*this)();
	}

	void start(uint32_t size) override {
		_size = size;
		resetBoard();
		std::cout << "OK" << std::endl;
	}

	void turn(uint32_t x, uint32_t y) override {
		NeuralNetwork::PossibleActions possibleActions;
		std::pair<uint32_t, uint32_t> action;

		_board[y][x][1] = 1.0f;
		possibleActions = getPossibleActions();
		action = _player(_board, possibleActions);
		_board[action.second][action.first][0] = 1.0f;
		std::cout << action.first << "," << action.second << std::endl;
	}

	void resetBoard() override {
		_board = getZerosMatrix<float>(_size, _size, 2);
	}

	void board(uint32_t x, uint32_t y, uint32_t player) override {
		_board[y][x][player] = 1.0f;
	}

	void info(const std::vector<std::string> &) override {}

	void end() override {
		std::exit(0);
	}

	void about() override {
		std::cout << std::string("name=\"ConvANN\", version=\"1.0\", ") +
			"author=\"Nymand\", \"country=\"USA\"" << std::endl;
	}

private:
	NeuralNetwork::PossibleActions getPossibleActions() const noexcept {
		std::vector<std::pair<uint32_t, uint32_t>> out;
		auto height = _size;
		auto width = _size;

		for (auto y = 0u; y < height; y++)
			for (auto x = 0u; x < width; x++)
				if (_board[y][x][0] == 0.0f &&
				    _board[y][x][1] == 0.0f)
					out.push_back(std::make_pair(x, y));
		return (out);
	}

	template <typename T>
	NeuralNetwork::Conv2DMatrix<T> getZerosMatrix(uint32_t width, uint32_t height,
		uint32_t channel) {
		std::vector<T> zeroChannel(channel, 0.0f);
		std::vector<std::vector<T>> zeroRow(width, zeroChannel);
		return (NeuralNetwork::Conv2DMatrix<T>(height, zeroRow));
	}

private:
	Board _board;
	uint32_t _size;
	NeuralNetwork::ANNPlayer<float> _player;
};
