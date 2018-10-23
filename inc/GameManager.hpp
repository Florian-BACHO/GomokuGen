//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// Game Manager
//

#pragma once

#include "AGameCommunication.hpp"

namespace Gomoku {
	class GameManager;
};

class Gomoku::GameManager : Gomoku::AGameCommunication {
public:
	GameManager()
		: AGameCommunication() {}

	void launchGame() {
		while (true)
			(*this)();
	}

	bool start(uint32_t size) override {
		_board = getZerosMatrix<float>(size, size, 2);
		return true;
	}

	bool turn(uint32_t x, uint32_t y) override {
		return true;
	}
};
