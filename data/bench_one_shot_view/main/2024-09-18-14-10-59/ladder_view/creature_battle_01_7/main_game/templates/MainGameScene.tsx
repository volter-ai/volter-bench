import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Heart, Swords, Shield } from 'lucide-react';

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
    <div className="container-[game] w-full h-full flex flex-col">
      <nav className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      <div className="flex-grow flex flex-col">
        <div className="flex-grow flex items-center justify-between p-4">
          {renderCreature(playerCreature, true)}
          {renderCreature(foeCreature, false)}
        </div>

        <div className="p-4 grid grid-cols-2 gap-2">
          {playerCreature.collections.skills.map((skill) => (
            <Button
              key={skill.uid}
              onClick={() => emitThingClick(skill.uid)}
              disabled={!availableInteractiveThingIds.includes(skill.uid)}
              className="flex items-center justify-center"
            >
              <Swords className="w-4 h-4 mr-2" />
              {skill.display_name}
            </Button>
          ))}
        </div>

        <div className="p-4 flex justify-center space-x-2">
          {['attack', 'defend', 'item', 'run'].map((action) => (
            <Button
              key={action}
              onClick={() => emitButtonClick(action)}
              disabled={!availableButtonSlugs.includes(action)}
              className="capitalize"
            >
              {action}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
}
