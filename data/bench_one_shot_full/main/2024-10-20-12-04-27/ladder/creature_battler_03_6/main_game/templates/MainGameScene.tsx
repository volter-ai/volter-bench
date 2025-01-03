import { useCurrentButtons } from "@/lib/useChoices.ts";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="flex flex-col h-screen w-full max-w-[177.78vh] mx-auto bg-gray-100">
      {/* HUD */}
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">Creature Battle</h1>
      </header>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-8">
        <div className="flex flex-col items-center">
          <span className="text-sm font-bold text-gray-700">Player</span>
          <PlayerCard
            uid={player.uid}
            playerName={player.display_name}
            imageUrl="/path/to/player/image.jpg"
            className="mb-4"
          />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl="/path/to/creature/image.jpg"
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <span className="text-sm font-bold text-gray-700">Opponent</span>
          <PlayerCard
            uid={opponent.uid}
            playerName={opponent.display_name}
            imageUrl="/path/to/opponent/image.jpg"
            className="mb-4"
          />
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl="/path/to/creature/image.jpg"
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4">
          <h2 className="text-xl font-bold mb-2">Creature Stats</h2>
          <div className="flex space-x-4">
            <div className="flex items-center">
              <Sword className="mr-1" size={16} />
              <span>Attack: {player_creature.stats.attack}</span>
            </div>
            <div className="flex items-center">
              <Shield className="mr-1" size={16} />
              <span>Defense: {player_creature.stats.defense}</span>
            </div>
            <div className="flex items-center">
              <Zap className="mr-1" size={16} />
              <span>Speed: {player_creature.stats.speed}</span>
            </div>
          </div>
        </div>
        <div>
          <h2 className="text-xl font-bold mb-2">Skills</h2>
          <div className="flex flex-wrap gap-2">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                className="bg-yellow-500 text-white px-4 py-2 rounded"
              />
            ))}
          </div>
        </div>
        <div className="mt-4">
          <div className="text-box mb-4 p-2 border rounded bg-gray-50">
            <p>Your turn to choose!</p>
          </div>
          <div className="flex space-x-2">
            {availableButtonSlugs.includes('play-again') && (
              <button
                className="bg-green-500 text-white px-4 py-2 rounded"
                onClick={() => emitButtonClick('play-again')}
              >
                Play Again
              </button>
            )}
            {availableButtonSlugs.includes('quit') && (
              <button
                className="bg-red-500 text-white px-4 py-2 rounded"
                onClick={() => emitButtonClick('quit')}
              >
                Quit
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
