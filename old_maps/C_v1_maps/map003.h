struct map003_struct {
	const static uint32_t world_y = 30;
	const static uint32_t world_x = 50;
	const static uint32_t world_n = 1500;

	const static uint8_t map[];
	const static uint8_t collision[];
	const static bool spawns[];

	const static uint32_t npc_n = 5;
	const static uint8_t npc_LUT[];
	const static uint8_t npc_move[];
	static const std::string npc_text[];
	const static uint32_t npc_pos[];
};
