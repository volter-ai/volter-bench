import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';

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
  skills: Array<{
    uid: string;
    display_name: string;
    description: string;
  }>;
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
    <div className="cq-w-full bg-gray-200 rounded-full cq-h-2.5 dark:bg-gray-700">
      <div 
        className="bg-blue-600 cq-h-2.5 rounded-full" 
        style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
      ></div>
    </div>
    <p>{creature.stats.hp} / {creature.stats.max_hp} HP</p>
  </Card>
);

const ActionButton = ({ slug, icon, label, uid }: { slug?: string; icon: React.ReactNode; label: string; uid?: string }) => {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();
  
  const isAvailable = slug ? availableButtonSlugs.includes(slug) : availableInteractiveThingIds.includes(uid);

  const handleClick = () => {
    if (slug) {
      emitButtonClick(slug);
    } else if (uid) {
      emitThingClick(uid);
    }
  };

  return (
    <Button 
      onClick={handleClick} 
      disabled={!isAvailable}
      className="cq-w-full cq-h-full flex flex-col items-center justify-center"
    >
      {icon}
      <span>{label}</span>
    </Button>
  );
};

export function MainGameSceneView(props: { data: GameUIData }) {
  const { data } = props;

  const playerCreature = data.entities.player.entities.active_creature;
  const botCreature = data.entities.bot.entities.active_creature;

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
      <div className="cq-h-[34%] grid grid-cols-2 grid-rows-2 gap-2 p-2">
        {(data.skills || []).map((skill, index) => (
          <ActionButton key={skill.uid} uid={skill.uid} icon={<Sword />} label={skill.display_name} />
        ))}
        <ActionButton slug="swap" icon={<Repeat />} label="Swap" />
        <ActionButton slug="back" icon={<ArrowLeft />} label="Back" />
      </div>
    </div>
  );
}
