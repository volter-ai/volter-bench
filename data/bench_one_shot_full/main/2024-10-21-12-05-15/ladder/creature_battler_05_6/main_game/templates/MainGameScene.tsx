import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { skill_type: string; is_physical: boolean };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number };
  meta: { creature_type: string };
  uid: string;
  display_name: string;
  description: string;
  collections: { skills: Skill[] };
}

interface Player {
  __type: "Player";
  entities: { active_creature: Creature };
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="w-full aspect-video bg-gray-100 flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Top-left: Opponent Status */}
          <div className="flex items-start justify-start">
            <PlayerCard
              uid={opponent.uid}
              playerName={opponent.display_name}
              imageUrl="/opponent-placeholder.png"
            />
          </div>

          {/* Top-right: Opponent Creature */}
          <div className="flex items-start justify-end">
            <CreatureCard
              uid={opponent.entities.active_creature?.uid || ""}
              name={opponent.entities.active_creature?.display_name || "Unknown"}
              image="/opponent-placeholder.png"
              hp={opponent.entities.active_creature?.stats.hp || 0}
              maxHp={opponent.entities.active_creature?.stats.max_hp || 1}
            />
          </div>

          {/* Bottom-left: Player Creature */}
          <div className="flex items-end justify-start">
            <CreatureCard
              uid={player.entities.active_creature?.uid || ""}
              name={player.entities.active_creature?.display_name || "Unknown"}
              image="/placeholder.png"
              hp={player.entities.active_creature?.stats.hp || 0}
              maxHp={player.entities.active_creature?.stats.max_hp || 1}
            />
          </div>

          {/* Bottom-right: Player Status */}
          <div className="flex items-end justify-end">
            <PlayerCard
              uid={player.uid}
              playerName={player.display_name}
              imageUrl="/player-placeholder.png"
            />
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-200 p-4">
          <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
            {availableButtonSlugs.includes("attack") && (
              <Button onClick={() => emitButtonClick("attack")}>
                <Sword className="mr-2 h-4 w-4" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes("back") && (
              <Button onClick={() => emitButtonClick("back")}>
                <ArrowLeft className="mr-2 h-4 w-4" /> Back
              </Button>
            )}
            {availableButtonSlugs.includes("swap") && (
              <Button onClick={() => emitButtonClick("swap")}>
                <Repeat className="mr-2 h-4 w-4" /> Swap
              </Button>
            )}
            {player.entities.active_creature?.collections.skills.map((skill) => (
              availableButtonSlugs.includes(skill.uid) && (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                  onClick={() => emitButtonClick(skill.uid)}
                />
              )
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
