import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, X } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  skills: Skill[];
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
  meta: {
    player_skill_selected: boolean;
    opponent_skill_selected: boolean;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <span>Player: {playerCreature?.display_name}</span>
        <span>VS</span>
        <span>Opponent: {opponentCreature?.display_name}</span>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature?.uid || "player-creature"}
          name={playerCreature?.display_name || "Unknown"}
          imageUrl="/placeholder-creature.jpg"
          hp={playerCreature?.stats.hp || 0}
        />
        <div className="text-4xl font-bold">VS</div>
        <CreatureCard
          uid={opponentCreature?.uid || "opponent-creature"}
          name={opponentCreature?.display_name || "Unknown"}
          imageUrl="/placeholder-creature.jpg"
          hp={opponentCreature?.stats.hp || 0}
        />
      </div>

      {/* User Interface */}
      <Card className="p-4 m-4 bg-white">
        {props.data.meta.player_skill_selected ? (
          <div className="text-center">
            Waiting for opponent to select a skill...
          </div>
        ) : (
          <div className="flex flex-wrap justify-center gap-2">
            {playerCreature?.skills && playerCreature.skills.length > 0 ? (
              playerCreature.skills.map((skill: Skill) => {
                const skillSlug = `use-skill-${skill.uid}`;
                return (
                  <SkillButton
                    key={skill.uid}
                    uid={skill.uid}
                    skillName={skill.display_name}
                    description={skill.description}
                    stats={`Damage: ${skill.stats.damage}`}
                    onClick={() => emitButtonClick(skillSlug)}
                    disabled={!availableButtonSlugs.includes(skillSlug)}
                  >
                    <Sword className="mr-2 h-4 w-4" />
                    {skill.display_name}
                  </SkillButton>
                );
              })
            ) : (
              <div className="text-center">No skills available</div>
            )}
            {availableButtonSlugs.includes('quit') && (
              <Button onClick={() => emitButtonClick('quit')} variant="destructive">
                <X className="mr-2 h-4 w-4" />
                Quit
              </Button>
            )}
          </div>
        )}
      </Card>
    </div>
  );
}
