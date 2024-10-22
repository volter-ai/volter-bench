import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full aspect-video bg-gray-100 flex flex-col">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div>{props.data.entities.player.display_name}</div>
        <div>{props.data.entities.opponent.display_name}</div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <div className="text-lg font-bold mb-2">Player</div>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder.png"
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
          <div className="mt-2 flex items-center">
            <Swords className="mr-1" /> {playerCreature.stats.attack}
            <Shield className="ml-2 mr-1" /> {playerCreature.stats.defense}
          </div>
        </div>
        <div className="flex flex-col items-center">
          <div className="text-lg font-bold mb-2">Opponent</div>
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/placeholder.png"
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
          <div className="mt-2 flex items-center">
            <Swords className="mr-1" /> {opponentCreature.stats.attack}
            <Shield className="ml-2 mr-1" /> {opponentCreature.stats.defense}
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white border-t-2 border-gray-300 p-4">
        <div className="flex flex-wrap justify-center gap-2">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
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
