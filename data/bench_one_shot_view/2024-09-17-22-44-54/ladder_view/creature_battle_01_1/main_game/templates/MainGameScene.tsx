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
  slug: string;
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
    <div className="w-full h-full flex flex-col">
      <nav className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <span>{props.data.entities.player.display_name}</span>
        <span>{props.data.entities.foe.display_name}</span>
      </nav>

      <div className="flex-grow flex flex-col justify-center p-4">
        <div className="flex justify-between mb-8">
          {renderCreature(foeCreature, false)}
        </div>
        <div className="flex justify-between mt-8">
          {renderCreature(playerCreature, true)}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-2 p-4 bg-gray-100">
        {playerCreature.collections.skills.map((skill) => (
          <Button
            key={skill.uid}
            onClick={() => emitButtonClick(skill.slug)}
            disabled={!availableButtonSlugs.includes(skill.slug)}
            className="flex items-center justify-center"
          >
            <Swords className="w-4 h-4 mr-2" />
            {skill.display_name}
          </Button>
        ))}
      </div>
    </div>
  );
}
