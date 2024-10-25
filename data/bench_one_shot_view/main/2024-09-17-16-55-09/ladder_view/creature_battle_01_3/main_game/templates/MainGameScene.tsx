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
  const { currentButtonIds, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  const renderCreature = (creature: Creature, isPlayer: boolean) => (
    <Card className={`p-4 ${isPlayer ? 'ml-auto' : 'mr-auto'} w-1/3`}>
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

      <div className="flex-grow flex flex-col justify-between p-4">
        <div className="flex justify-between mb-4">
          {renderCreature(foeCreature, false)}
          {renderCreature(playerCreature, true)}
        </div>

        <div className="grid grid-cols-2 gap-4 mt-auto">
          {playerCreature.collections.skills.length > 0 ? (
            playerCreature.collections.skills.map((skill) => (
              <Button
                key={skill.uid}
                onClick={() => emitThingClick(skill.uid)}
                disabled={!availableInteractiveThingIds.includes(skill.uid)}
                className="p-2 text-left"
              >
                <div className="flex items-center">
                  <Swords className="w-4 h-4 mr-2" />
                  <div>
                    <div className="font-bold">{skill.display_name}</div>
                    <div className="text-sm">{skill.description}</div>
                  </div>
                </div>
              </Button>
            ))
          ) : (
            <div className="col-span-2 text-center text-gray-500">
              No skills available
            </div>
          )}
        </div>
      </div>

      {currentButtonIds.includes('tackle') && (
        <Alert className="mt-4">
          <AlertTitle>Combat Action</AlertTitle>
          <AlertDescription>
            Use Tackle to attack your opponent!
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
}
