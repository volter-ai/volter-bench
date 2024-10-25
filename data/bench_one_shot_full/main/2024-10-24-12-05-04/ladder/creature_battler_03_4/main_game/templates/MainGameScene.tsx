import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword, Zap } from 'lucide-react';
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  collections?: {
    skills?: Skill[];
  };
}

interface Player {
  __type: "Player";
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
  const { availableButtonSlugs } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={props.data.entities.player.uid}
          playerName={props.data.entities.player.display_name}
          imageUrl="/path/to/player-image.png"
        />
        <div className="flex space-x-4">
          <div className="flex items-center">
            <Shield className="mr-1" /> {playerCreature.stats.defense}
          </div>
          <div className="flex items-center">
            <Sword className="mr-1" /> {playerCreature.stats.attack}
          </div>
          <div className="flex items-center">
            <Zap className="mr-1" /> {playerCreature.stats.speed}
          </div>
        </div>
        <PlayerCard
          uid={props.data.entities.opponent.uid}
          playerName={props.data.entities.opponent.display_name}
          imageUrl="/path/to/opponent-image.png"
        />
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="relative">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/path/to/player-creature-image.png"
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
          <div className="absolute top-0 left-0 bg-blue-500 text-white px-2 py-1 rounded-br-md">
            Player
          </div>
        </div>
        <div className="relative">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/path/to/opponent-creature-image.png"
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
          <div className="absolute top-0 right-0 bg-red-500 text-white px-2 py-1 rounded-bl-md">
            Opponent
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
