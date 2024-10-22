import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayCircle, XCircle } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  uid: string;
  display_name: string;
  description: string;
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  description: string;
  collections: {
    creatures: Creature[];
  };
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

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col aspect-[16/9] max-w-full max-h-full bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature?.uid ?? ""}
          name={playerCreature?.display_name ?? "Unknown"}
          imageUrl="/placeholder-creature.png"
          hp={playerCreature?.stats.hp ?? 0}
          maxHp={playerCreature?.stats.max_hp ?? 1}
          className="transform scale-x-[-1]"
        />
        <CreatureCard
          uid={opponentCreature?.uid ?? ""}
          name={opponentCreature?.display_name ?? "Unknown"}
          imageUrl="/placeholder-creature.png"
          hp={opponentCreature?.stats.hp ?? 0}
          maxHp={opponentCreature?.stats.max_hp ?? 1}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
            />
          ))}
          {availableButtonSlugs.includes("play-again") && (
            <button
              onClick={() => emitButtonClick("play-again")}
              className="flex items-center bg-green-500 text-white px-4 py-2 rounded"
            >
              <PlayCircle className="mr-2" /> Play Again
            </button>
          )}
          {availableButtonSlugs.includes("quit") && (
            <button
              onClick={() => emitButtonClick("quit")}
              className="flex items-center bg-red-500 text-white px-4 py-2 rounded"
            >
              <XCircle className="mr-2" /> Quit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
