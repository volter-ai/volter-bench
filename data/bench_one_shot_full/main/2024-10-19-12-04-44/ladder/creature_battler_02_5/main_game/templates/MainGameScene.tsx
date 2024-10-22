import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={props.data.entities.player.uid}
          playerName={props.data.entities.player.display_name}
          imageUrl="/path/to/player/image.jpg"
        />
        <PlayerCard
          uid={props.data.entities.opponent.uid}
          playerName={props.data.entities.opponent.display_name}
          imageUrl="/path/to/opponent/image.jpg"
        />
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/path/to/player/creature/image.jpg"
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <Shield className="text-blue-500" />
            <span>{playerCreature.stats.defense}</span>
            <Swords className="text-red-500" />
            <span>{playerCreature.stats.attack}</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/path/to/opponent/creature/image.jpg"
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <Shield className="text-blue-500" />
            <span>{opponentCreature.stats.defense}</span>
            <Swords className="text-red-500" />
            <span>{opponentCreature.stats.attack}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="mb-4 h-24 bg-gray-200 p-2 rounded">
          {/* Text display area for game messages */}
          <p>Game messages will be displayed here.</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={`skill-${skill.uid}`}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
