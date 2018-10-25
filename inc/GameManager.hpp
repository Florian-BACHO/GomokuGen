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
#include <random>
#include <ctime>
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
		if (checkComplete())
			return;
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

	void begin() override {
		auto x = randint(0, _size - 1);
		auto y = randint(0, _size - 1);

		_board[y][x][0] = 1.0f;
		std::cout << x << "," << y << std::endl;
	}

private:
	inline uint32_t randint(uint32_t min, uint32_t max) {
		std::mt19937 rng(static_cast<unsigned int>(std::time(nullptr)));
		std::uniform_int_distribution<uint32_t> gen(min, max);

		return (gen(rng));
	}

	inline bool isEmpty(uint32_t x, uint32_t y) const noexcept {
		return (_board[y][x][0] == 0.0f && _board[y][x][1] == 0.0f);
	}

	NeuralNetwork::PossibleActions getPossibleActions() const noexcept {
		std::vector<std::pair<uint32_t, uint32_t>> out;
		auto height = _size;
		auto width = _size;

		for (auto y = 0u; y < height; y++)
			for (auto x = 0u; x < width; x++)
				if (isEmpty(x, y))
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

	bool playIfEmpty(uint32_t x, uint32_t y) const noexcept {
		if (x >= _size || y >= _size || !isEmpty(x, y))
			return false;
		std::cout << x << "," << y << std::endl;
		return true;
	}

	bool checkComplete() const noexcept {
		for (auto y = 0u; y < _size; y++)
			for (auto x = 0u; x < _size; x++)
				if (checkVertical(x, y) ||
					checkHorizontal(x, y) ||
					checkDiagLeft(x, y) ||
					checkDiagRight(x, y))
					return true;
		return false;
	}

	bool checkVertical(uint32_t x, uint32_t y) const noexcept {
		uint32_t counter = 0;
		int32_t xTarget = -1;
		int32_t yTarget = -1;

		for (auto y2 = y; y2 < y + 5; y2++) {
			if (y2 >= _size)
				break;
			if (isEmpty(x, y2) && xTarget == -1) {
				xTarget = x;
				yTarget = y2;
			} else if ((isEmpty(x, y2) && xTarget != -1) || _board[y2][x][1] == 1.0f)
				break;
			else
				counter++;
		}
		if (counter == 4 && xTarget != -1) {
			std::cout << xTarget << "," << yTarget << std::endl;
			return true;
		}
		return false;
	}

	bool checkHorizontal(uint32_t x, uint32_t y) const noexcept {
		uint32_t counter = 0;
		int32_t xTarget = -1;
		int32_t yTarget = -1;

		for (auto x2 = x; x2 < x + 5; x2++) {
			if (x2 >= _size)
				break;
			if (isEmpty(x2, y) && xTarget == -1) {
				xTarget = x2;
				yTarget = y;
			}
			else if ((isEmpty(x2, y) && xTarget != -1) || _board[y][x2][1] == 1.0f)
				break;
			else
				counter++;
		}
		if (counter == 4 && xTarget != -1) {
			std::cout << xTarget << "," << yTarget << std::endl;
			return true;
		}
		return false;
	}

	bool checkDiagRight(uint32_t x, uint32_t y) const noexcept {
		uint32_t counter = 0;
		auto y2 = y;
		int32_t xTarget = -1;
		int32_t yTarget = -1;

		for (auto x2 = x; x2 < x + 5; x2++) {
			if (x2 >= _size || y2 >= _size)
				break;
			if (isEmpty(x2, y2) && xTarget == -1) {
				xTarget = x2;
				yTarget = y2;
			}
			else if ((isEmpty(x2, y2) && xTarget != -1) || _board[y2][x2][1] == 1.0f)
				break;
			else
				counter++;
			y2--;
		}
		if (counter == 4 && xTarget != -1) {
			std::cout << xTarget << "," << yTarget << std::endl;
			return true;
		}
		return false;
	}

	bool checkDiagLeft(uint32_t x, uint32_t y) const noexcept {
		uint32_t counter = 0;
		auto y2 = y;
		int32_t xTarget = -1;
		int32_t yTarget = -1;

		for (auto x2 = x; x2 < x + 5; x2++) {
			if (x2 >= _size || y2 >= _size)
				break;
			if (isEmpty(x2, y2) && xTarget == -1) {
				xTarget = x2;
				yTarget = y2;
			}
			else if ((isEmpty(x2, y2) && xTarget != -1) || _board[y2][x2][1] == 1.0f)
				break;
			else
				counter++;
			y2++;
		}
		if (counter == 4 && xTarget != -1) {
			std::cout << xTarget << "," << yTarget << std::endl;
			return true;
		}
		return false;
	}

private:
	Board _board;
	uint32_t _size;
	NeuralNetwork::ANNPlayer<float> _player;
};
