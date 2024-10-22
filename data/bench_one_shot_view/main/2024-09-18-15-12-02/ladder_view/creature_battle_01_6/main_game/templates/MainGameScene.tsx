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
    <div className="cq-h-full cq-w-full cq-flex cq-flex-col cq-bg-gray-100">
      <nav className="cq-w-full cq-bg-blue-600 cq-text-white cq-p-4">
        <h1 className="cq-text-2xl cq-font-bold">Creature Battle</h1>
      </nav>

      <div className="cq-flex-grow cq-flex cq-flex-col cq-justify-center cq-p-4">
        <div className="cq-grid cq-grid-cols-2 cq-gap-4">
          <Card className="cq-p-4">
            <h2 className="cq-text-xl cq-font-bold">{playerCreature?.display_name}</h2>
            <p>HP: {playerCreature?.stats.hp} / {playerCreature?.stats.max_hp}</p>
            <div className="cq-flex cq-items-center cq-mt-2">
              <Heart className="cq-w-5 cq-h-5 cq-text-red-500 cq-mr-2" />
              <div className="cq-bg-gray-200 cq-w-full cq-h-4 cq-rounded-full">
                <div
                  className="cq-bg-red-500 cq-h-full cq-rounded-full"
                  style={{ width: `${(playerCreature?.stats.hp / playerCreature?.stats.max_hp) * 100}%` }}
                ></div>
              </div>
            </div>
          </Card>
          <Card className="cq-p-4">
            <h2 className="cq-text-xl cq-font-bold">{foeCreature?.display_name}</h2>
            <p>HP: {foeCreature?.stats.hp} / {foeCreature?.stats.max_hp}</p>
            <div className="cq-flex cq-items-center cq-mt-2">
              <Heart className="cq-w-5 cq-h-5 cq-text-red-500 cq-mr-2" />
              <div className="cq-bg-gray-200 cq-w-full cq-h-4 cq-rounded-full">
                <div
                  className="cq-bg-red-500 cq-h-full cq-rounded-full"
                  style={{ width: `${(foeCreature?.stats.hp / foeCreature?.stats.max_hp) * 100}%` }}
                ></div>
              </div>
            </div>
          </Card>
        </div>
      </div>

      <div className="cq-p-4 cq-bg-gray-200">
        <h3 className="cq-text-lg cq-font-bold cq-mb-2">Actions</h3>
        <div className="cq-grid cq-grid-cols-2 cq-gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <Button
              key={skill.uid}
              onClick={() => emitThingClick(skill.uid)}
              disabled={!availableInteractiveThingIds.includes(skill.uid)}
              className="cq-flex cq-items-center cq-justify-center"
            >
              <Swords className="cq-w-5 cq-h-5 cq-mr-2" />
              {skill.display_name}
            </Button>
          ))}
          <Button
            onClick={() => emitButtonClick('defend')}
            disabled={!availableButtonSlugs.includes('defend')}
            className="cq-flex cq-items-center cq-justify-center"
          >
            <Shield className="cq-w-5 cq-h-5 cq-mr-2" />
            Defend
          </Button>
        </div>
      </div>
    </div>
  );
}
