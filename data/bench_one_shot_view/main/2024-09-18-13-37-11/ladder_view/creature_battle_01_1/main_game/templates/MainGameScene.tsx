import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Heart, Zap } from 'lucide-react';

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

  return (
    <div className="container-query:w-full container-query:h-full flex flex-col">
      {/* HUD */}
      <nav className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <div>{props.data.entities.player.display_name}</div>
        <div>{props.data.entities.foe.display_name}</div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {/* Player Creature */}
        <Card className="w-1/3 p-4">
          <h2 className="text-xl font-bold">{playerCreature.display_name}</h2>
          <div className="flex items-center mt-2">
            <Heart className="mr-2" />
            <div>{playerCreature.stats.hp} / {playerCreature.stats.max_hp}</div>
          </div>
        </Card>

        {/* Opponent Creature */}
        <Card className="w-1/3 p-4">
          <h2 className="text-xl font-bold">{foeCreature.display_name}</h2>
          <div className="flex items-center mt-2">
            <Heart className="mr-2" />
            <div>{foeCreature.stats.hp} / {foeCreature.stats.max_hp}</div>
          </div>
        </Card>
      </div>

      {/* Choices */}
      <div className="p-4 bg-gray-100">
        <h3 className="text-lg font-semibold mb-2">Skills</h3>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature.collections.skills.map((skill) => (
            <Button
              key={skill.uid}
              className="w-full"
              onClick={() => emitThingClick(skill.uid)}
              disabled={!availableInteractiveThingIds.includes(skill.uid)}
            >
              <div className="flex items-center">
                <Zap className="mr-2" />
                <div>
                  <div>{skill.display_name}</div>
                  <div className="text-sm text-gray-500">Damage: {skill.stats.damage}</div>
                </div>
              </div>
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
}
