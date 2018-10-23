//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// main
//

#include "GameManager.hpp"

#ifdef  _WIN32
int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
	PSTR lpCmdLine, INT nCmdShow) {
#else
int main()
{
#endif
	Gomoku::GameManager manager;

	manager.launchGame();
	return (0);
}
