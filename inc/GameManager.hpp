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

	bool start(uint32_t, uint32_t) override {
		std::cerr << "Called start" << std::endl;
		return true;
	}
};
