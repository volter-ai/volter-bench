import { useCurrentButtons } from "@/lib/useChoices.ts";
import { ArrowLeft } from 'lucide-react';
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { prototype_id: string; category: string; skill_type: string };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number; attack: number; defense: number; speed: number };
  meta: { prototype_id: string; category: string; creature_type: string };
  collections: { skills: Skill[] };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  meta: { prototype_id: string; category: string };
  collections: { creatures: Creature[] };
  uid: string;
  display_name: string;
  description: string;
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

  const renderButtons = () => {
    return availableButtonSlugs.map((slug) => (
      <Button
        key={slug}
        onClick={() => emitButtonClick(slug)}
        className="m-1"
      >
        {slug === "return-to-main-menu" ? (
          <>
            <ArrowLeft className="mr-2 h-4 w-4" /> Return to Main Menu
          </>
        ) : (
          slug
        )}
      </Button>
    ));
  };

  return (
    <div className="flex flex-col h-full w-full bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Pokemon-like Creature Battler</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {/* Player Creature */}
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={props.data.entities.player_creature?.uid || ""}
            name={props.data.entities.player_creature?.display_name || "Unknown"}
            imageUrl="/placeholder-creature.png"
            hp={props.data.entities.player_creature?.stats.hp || 0}
            maxHp={props.data.entities.player_creature?.stats.max_hp || 1}
          />
          <p className="mt-2 font-bold">Player's Creature</p>
        </div>

        {/* Opponent Creature */}
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={props.data.entities.opponent_creature?.uid || ""}
            name={props.data.entities.opponent_creature?.display_name || "Unknown"}
            imageUrl="/placeholder-creature.png"
            hp={props.data.entities.opponent_creature?.stats.hp || 0}
            maxHp={props.data.entities.opponent_creature?.stats.max_hp || 1}
          />
          <p className="mt-2 font-bold">Opponent's Creature</p>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4">
          <h2 className="text-lg font-bold mb-2">Player's Skills</h2>
          <div className="flex flex-wrap">
            {props.data.entities.player_creature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.uid)}
                className="m-1"
              />
            ))}
          </div>
        </div>
        <div>
          <h2 className="text-lg font-bold mb-2">Game Controls</h2>
          <div className="flex flex-wrap">
            {renderButtons()}
          </div>
        </div>
      </div>
    </div>
  );
}
