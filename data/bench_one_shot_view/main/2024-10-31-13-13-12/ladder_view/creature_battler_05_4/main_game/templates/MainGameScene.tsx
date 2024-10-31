import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

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
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  entities: {
    active_creature: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent Creature */}
        {opponentCreature && (
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/placeholder-opponent.png"
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            className="justify-self-start"
          />
        )}

        {/* Top-right: Opponent Status */}
        <div className="flex flex-col items-end justify-start">
          <h3 className="text-xl font-bold">{opponentCreature?.display_name}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className="bg-red-600 h-2.5 rounded-full"
              style={{ width: `${(opponentCreature?.stats.hp / opponentCreature?.stats.max_hp) * 100 || 0}%` }}
            ></div>
          </div>
          <span>{opponentCreature?.stats.hp}/{opponentCreature?.stats.max_hp} HP</span>
        </div>

        {/* Bottom-left: Player Status */}
        <div className="flex flex-col items-start justify-end">
          <h3 className="text-xl font-bold">{playerCreature?.display_name}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className="bg-green-600 h-2.5 rounded-full"
              style={{ width: `${(playerCreature?.stats.hp / playerCreature?.stats.max_hp) * 100 || 0}%` }}
            ></div>
          </div>
          <span>{playerCreature?.stats.hp}/{playerCreature?.stats.max_hp} HP</span>
        </div>

        {/* Bottom-right: Player Creature */}
        {playerCreature && (
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-player.png"
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            className="justify-self-end self-end"
          />
        )}
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4 flex flex-col justify-center">
        <div className="flex flex-wrap gap-2 justify-center">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')}>
              Attack
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              Swap
            </Button>
          )}
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
