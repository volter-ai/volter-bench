import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield, Swords } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
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
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full aspect-video bg-gray-100 flex flex-col">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center px-4">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={playerCreature?.uid || "player-creature"}
            name={playerCreature?.display_name || "Player Creature"}
            imageUrl="/placeholder-creature.jpg"
            hp={playerCreature?.stats.hp || 0}
          />
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={opponentCreature?.uid || "opponent-creature"}
            name={opponentCreature?.display_name || "Opponent Creature"}
            imageUrl="/placeholder-creature.jpg"
            hp={opponentCreature?.stats.hp || 0}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4">
        <Card className="mb-4 p-2">
          <p>Battle description goes here...</p>
        </Card>
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
          {availableButtonSlugs.includes("play-again") && (
            <Button onClick={() => emitButtonClick("play-again")}>
              Play Again
            </Button>
          )}
          {availableButtonSlugs.includes("quit") && (
            <Button onClick={() => emitButtonClick("quit")}>
              Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
