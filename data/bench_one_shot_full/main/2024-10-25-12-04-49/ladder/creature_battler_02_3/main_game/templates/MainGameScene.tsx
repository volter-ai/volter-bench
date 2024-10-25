import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Sword, Shield, Zap } from 'lucide-react';

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
    <div className="w-full h-full aspect-[16/9] bg-gray-100 flex flex-col">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature.uid}
          name={playerCreature.display_name}
          imageUrl="/placeholder-creature.png"
          hp={playerCreature.stats.hp}
          maxHp={playerCreature.stats.max_hp}
          className="transform scale-x-[-1]"
        />
        <div className="flex flex-col items-center">
          <Sword className="w-8 h-8 mb-2" />
          <Shield className="w-8 h-8 mb-2" />
          <Zap className="w-8 h-8" />
        </div>
        <CreatureCard
          uid={opponentCreature.uid}
          name={opponentCreature.display_name}
          imageUrl="/placeholder-creature.png"
          hp={opponentCreature.stats.hp}
          maxHp={opponentCreature.stats.max_hp}
        />
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4 h-1/3">
        <div className="mb-4">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              className="mr-2 mb-2"
            />
          ))}
        </div>
        <div>
          {availableButtonSlugs.includes("play-again") && (
            <Button
              onClick={() => emitButtonClick("play-again")}
              className="mr-2"
            >
              Play Again
            </Button>
          )}
          {availableButtonSlugs.includes("quit-game") && (
            <Button
              onClick={() => emitButtonClick("quit-game")}
              variant="destructive"
            >
              Quit Game
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
