import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { useState } from 'react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  entities: {
    active_creature: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
  };
}

const CreatureDisplay = ({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) => (
  <div className={`cq-w-1/2 cq-h-full flex ${isPlayer ? 'items-end' : 'items-start'} justify-center`}>
    <div className="cq-w-32 cq-h-32 bg-gray-300 rounded-full flex items-center justify-center">
      {creature.display_name[0]}
    </div>
  </div>
);

const CreatureStatus = ({ creature }: { creature: Creature }) => (
  <Card className="cq-w-1/2 cq-p-2">
    <h3 className="text-lg font-bold">{creature.display_name}</h3>
    <div className="cq-w-full bg-gray-200 rounded-full cq-h-2.5">
      <div
        className="bg-blue-600 cq-h-2.5 rounded-full"
        style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
      ></div>
    </div>
    <p>{creature.stats.hp} / {creature.stats.max_hp} HP</p>
  </Card>
);

const ActionButtons = ({ availableButtonSlugs, emitButtonClick, setShowSkills }: { availableButtonSlugs: string[], emitButtonClick: (slug: string) => void, setShowSkills: (show: boolean) => void }) => (
  <div className="grid grid-cols-2 gap-2 cq-p-4">
    {['attack', 'back', 'swap'].map((action) => (
      <Button
        key={action}
        onClick={() => {
          if (action === 'attack') {
            setShowSkills(true);
          } else {
            emitButtonClick(action);
          }
        }}
        disabled={!availableButtonSlugs.includes(action)}
        className="cq-h-12"
        data-testid={`button-${action}`}
      >
        {action === 'attack' && <Sword className="mr-2" />}
        {action === 'back' && <ArrowLeft className="mr-2" />}
        {action === 'swap' && <Repeat className="mr-2" />}
        {action.charAt(0).toUpperCase() + action.slice(1)}
      </Button>
    ))}
  </div>
);

const SkillList = ({ creature, emitThingClick, setShowSkills }: { creature: Creature, emitThingClick: (uid: string) => void, setShowSkills: (show: boolean) => void }) => (
  <div className="cq-p-4">
    <h3 className="text-lg font-bold mb-2">Select a skill:</h3>
    {creature.collections.skills.map((skill) => (
      <Button
        key={skill.uid}
        onClick={() => {
          emitThingClick(skill.uid);
          setShowSkills(false);
        }}
        className="cq-w-full cq-mb-2"
        data-testid={`skill-${skill.uid}`}
      >
        {skill.display_name}
      </Button>
    ))}
    <Button onClick={() => setShowSkills(false)} className="cq-w-full">Back</Button>
  </div>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();
  const [showSkills, setShowSkills] = useState(false);

  const playerCreature = props.data.entities.player.entities.active_creature;
  const botCreature = props.data.entities.bot.entities.active_creature;

  const handleButtonClick = (slug: string) => {
    if (slug === 'attack') {
      setShowSkills(true);
    } else {
      emitButtonClick(slug);
    }
  };

  return (
    <div className="cq-w-full cq-h-full flex flex-col">
      <div className="cq-h-[66%] flex flex-col">
        <div className="cq-h-1/2 flex">
          <CreatureStatus creature={botCreature} />
          <CreatureDisplay creature={botCreature} isPlayer={false} />
        </div>
        <div className="cq-h-1/2 flex flex-row-reverse">
          <CreatureStatus creature={playerCreature} />
          <CreatureDisplay creature={playerCreature} isPlayer={true} />
        </div>
      </div>
      <div className="cq-h-[34%] bg-gray-100">
        {showSkills ? (
          <SkillList creature={playerCreature} emitThingClick={emitThingClick} setShowSkills={setShowSkills} />
        ) : (
          <ActionButtons
            availableButtonSlugs={availableButtonSlugs}
            emitButtonClick={handleButtonClick}
            setShowSkills={setShowSkills}
          />
        )}
      </div>
    </div>
  );
}
