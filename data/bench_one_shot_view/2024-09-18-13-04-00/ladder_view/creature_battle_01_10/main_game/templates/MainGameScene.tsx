import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Sword, Shield, Heart } from 'lucide-react';

interface Skill {
  uid: string;
  slug: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Creature {
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
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
  };
}

const BattlefieldDisplay: React.FC<{ creature: Creature; isPlayer: boolean }> = ({ creature, isPlayer }) => (
  <Card className="flex flex-col items-center p-4 @container">
    <h2 className="text-lg font-bold mb-2">{creature.display_name}</h2>
    <p className="text-sm mb-2">{creature.description}</p>
    <div className="flex items-center">
      <Heart className="w-4 h-4 mr-1" />
      <span>{creature.stats.hp} / {creature.stats.max_hp}</span>
    </div>
    <div className="mt-4 cq:w-32 cq:h-32 cq:sm:w-48 cq:sm:h-48 bg-gray-200 rounded-full flex items-center justify-center">
      {isPlayer ? '🧑' : '🤖'}
    </div>
  </Card>
);

const HUD: React.FC<{ player: Player }> = ({ player }) => (
  <nav className="bg-gray-800 text-white p-2 flex justify-between items-center">
    <span>{player.display_name}</span>
    <div className="flex items-center">
      <Sword className="w-4 h-4 mr-1" />
      <span className="mr-4">Attack</span>
      <Shield className="w-4 h-4 mr-1" />
      <span>Defense</span>
    </div>
  </nav>
);

const SkillButton: React.FC<{ skill: Skill; onClick: () => void; isAvailable: boolean }> = ({ skill, onClick, isAvailable }) => (
  <Button
    onClick={onClick}
    disabled={!isAvailable}
    className={`m-1 p-2 flex flex-col items-center ${!isAvailable ? 'opacity-50 cursor-not-allowed' : ''}`}
  >
    <span>{skill.display_name}</span>
    <small>{skill.description}</small>
    <span>Damage: {skill.stats.damage}</span>
  </Button>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  console.log("Available button slugs:", availableButtonSlugs);

  return (
    <div className="flex flex-col h-full @container">
      <HUD player={props.data.entities.player} />
      <div className="flex-grow flex flex-col justify-center items-center p-4">
        <div className="flex justify-between w-full mb-8">
          <BattlefieldDisplay creature={foeCreature} isPlayer={false} />
          <BattlefieldDisplay creature={playerCreature} isPlayer={true} />
        </div>
        <Card className="w-full p-4">
          <h3 className="text-lg font-bold mb-2">Skills</h3>
          <div className="flex flex-wrap justify-center">
            {playerCreature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                skill={skill}
                onClick={() => {
                  console.log(`Button clicked: ${skill.slug}`);
                  emitButtonClick(skill.slug);
                }}
                isAvailable={availableButtonSlugs.includes(skill.slug)}
              />
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
