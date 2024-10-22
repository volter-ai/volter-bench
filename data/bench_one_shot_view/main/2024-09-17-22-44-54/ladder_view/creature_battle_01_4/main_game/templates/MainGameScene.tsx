import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Heart, Swords } from 'lucide-react';

interface Skill {
  uid: string;
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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  const renderCreature = (creature: Creature, isPlayer: boolean) => (
    <Card className={`p-4 ${isPlayer ? 'ml-auto' : 'mr-auto'}`}>
      <h3 className="text-lg font-bold">{creature.display_name}</h3>
      <div className="flex items-center mt-2">
        <Heart className="w-4 h-4 mr-1" />
        <span>{creature.stats.hp} / {creature.stats.max_hp}</span>
      </div>
    </Card>
  );

  return (
    <div className="@container w-full h-full flex flex-col">
      <nav className="bg-gray-800 text-white p-2">
        <h2 className="text-xl font-bold">Battle Arena</h2>
      </nav>

      <div className="flex-grow flex items-center justify-between p-4">
        {renderCreature(playerCreature, true)}
        <Swords className="w-8 h-8 mx-4" />
        {renderCreature(foeCreature, false)}
      </div>

      <div className="grid grid-cols-2 gap-2 p-4">
        {playerCreature.collections.skills.map((skill) => (
          <Button
            key={skill.uid}
            onClick={() => emitThingClick(skill.uid)}
            disabled={!availableInteractiveThingIds.includes(skill.uid)}
            className="w-full"
          >
            <div className="text-left">
              <div className="font-bold">{skill.display_name}</div>
              <div className="text-sm">{skill.description}</div>
              <div className="text-xs">Damage: {skill.stats.damage}</div>
            </div>
          </Button>
        ))}
      </div>

      {availableButtonSlugs.includes('tackle') && (
        <Button
          onClick={() => emitButtonClick('tackle')}
          className="mt-2 mx-auto"
        >
          Tackle
        </Button>
      )}
    </div>
  );
}
