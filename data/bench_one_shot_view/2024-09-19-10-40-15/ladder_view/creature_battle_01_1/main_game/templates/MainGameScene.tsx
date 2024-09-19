import {useCurrentButtons, useThingInteraction} from "@/lib/useChoices.ts";
import {Card} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {Alert, AlertTitle, AlertDescription} from "@/components/ui/alert";
import { Heart, Swords } from 'lucide-react'

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
      <nav className="bg-gray-800 text-white p-2 @sm:p-4">
        <h1 className="text-xl @sm:text-2xl font-bold">Creature Battle</h1>
      </nav>

      <div className="flex-grow flex flex-col @sm:flex-row items-center justify-center p-4 bg-green-100">
        <div className="w-full @sm:w-1/2 mb-4 @sm:mb-0">
          {renderCreature(playerCreature, true)}
        </div>
        <div className="w-full @sm:w-1/2">
          {renderCreature(foeCreature, false)}
        </div>
      </div>

      <div className="p-4 bg-gray-100">
        <h2 className="text-lg font-bold mb-2">Skills</h2>
        <div className="grid grid-cols-2 @sm:grid-cols-4 gap-2">
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
      </div>
    </div>
  );
}
