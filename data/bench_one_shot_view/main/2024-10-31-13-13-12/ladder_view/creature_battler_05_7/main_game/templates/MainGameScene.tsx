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
        {/* Top-left: Opponent Status */}
        <div className="flex flex-col items-start">
          <h3 className="text-xl font-bold">{opponentCreature?.display_name}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className="bg-red-600 h-2.5 rounded-full"
              style={{ width: `${(opponentCreature?.stats.hp / opponentCreature?.stats.max_hp) * 100 || 0}%` }}
            ></div>
          </div>
          <span>{opponentCreature?.stats.hp}/{opponentCreature?.stats.max_hp} HP</span>
        </div>

        {/* Top-right: Opponent Creature */}
        {opponentCreature && (
          <div className="justify-self-end">
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl="/placeholder-opponent.png"
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          </div>
        )}

        {/* Bottom-left: Player Creature */}
        {playerCreature && (
          <div className="self-end">
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="/placeholder-player.png"
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          </div>
        )}

        {/* Bottom-right: Player Status */}
        <div className="flex flex-col items-end self-end">
          <h3 className="text-xl font-bold">{playerCreature?.display_name}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className="bg-green-600 h-2.5 rounded-full"
              style={{ width: `${(playerCreature?.stats.hp / playerCreature?.stats.max_hp) * 100 || 0}%` }}
            ></div>
          </div>
          <span>{playerCreature?.stats.hp}/{playerCreature?.stats.max_hp} HP</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4 flex flex-col justify-center">
        <div className="flex flex-wrap gap-2 justify-center">
          {availableButtonSlugs.map((slug) => {
            if (slug === 'attack' || slug === 'swap') {
              return (
                <Button key={slug} onClick={() => emitButtonClick(slug)}>
                  {slug.charAt(0).toUpperCase() + slug.slice(1)}
                </Button>
              );
            }
            const skill = playerCreature?.collections.skills.find(
              (s) => s.display_name.toLowerCase() === slug
            );
            if (skill) {
              return (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Base Damage: ${skill.stats.base_damage}`}
                  onClick={() => emitButtonClick(slug)}
                />
              );
            }
            return null;
          })}
        </div>
      </div>
    </div>
  );
}
