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

  return (
    <div className="container-[game] w-full h-full flex flex-col">
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <div>{props.data.entities.player.display_name}</div>
        <div>{props.data.entities.foe.display_name}</div>
      </div>

      <div className="flex-grow grid grid-cols-2 gap-4 p-4">
        <Card className="p-4 flex flex-col justify-between">
          <div>
            <h2 className="text-xl font-bold">{playerCreature?.display_name}</h2>
            <p>HP: {playerCreature?.stats.hp} / {playerCreature?.stats.max_hp}</p>
          </div>
          <div className="mt-2">
            {playerCreature?.collections.skills.map((skill) => (
              <Button
                key={skill.uid}
                className="mr-2 mb-2"
                onClick={() => emitThingClick(skill.uid)}
                disabled={!availableInteractiveThingIds.includes(skill.uid)}
              >
                {skill.display_name}
              </Button>
            ))}
          </div>
        </Card>

        <Card className="p-4 flex flex-col justify-between">
          <div>
            <h2 className="text-xl font-bold">{foeCreature?.display_name}</h2>
            <p>HP: {foeCreature?.stats.hp} / {foeCreature?.stats.max_hp}</p>
          </div>
        </Card>
      </div>

      <div className="bg-gray-200 p-4 flex justify-center">
        {availableButtonSlugs.includes('attack') && (
          <Button className="mx-2" onClick={() => emitButtonClick('attack')}>
            <Swords className="mr-2 h-4 w-4" /> Attack
          </Button>
        )}
        {availableButtonSlugs.includes('defend') && (
          <Button className="mx-2" onClick={() => emitButtonClick('defend')}>
            <Shield className="mr-2 h-4 w-4" /> Defend
          </Button>
        )}
        {availableButtonSlugs.includes('heal') && (
          <Button className="mx-2" onClick={() => emitButtonClick('heal')}>
            <Heart className="mr-2 h-4 w-4" /> Heal
          </Button>
        )}
      </div>
    </div>
  );
}
