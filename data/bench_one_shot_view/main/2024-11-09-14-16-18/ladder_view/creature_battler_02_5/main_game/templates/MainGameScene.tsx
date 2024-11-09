import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button"; 
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  description: string;
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

const CreatureDisplay = ({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) => (
  <Card className="flex flex-col items-center p-4">
    <h3 className="text-lg font-bold mb-2">{creature.display_name}</h3>
    <Card className="w-48 h-48 flex items-center justify-center bg-slate-700">
      <span className="text-white">{isPlayer ? "Player's" : "Opponent's"} {creature.display_name}</span>
    </Card>
    <div className="mt-4 flex gap-2 items-center">
      <Heart className="text-red-500" />
      <span>
        {creature.stats.hp}/{creature.stats.max_hp}
      </span>
    </div>
    <div className="flex gap-4 mt-2">
      <div className="flex items-center gap-1">
        <Sword className="w-4 h-4" />
        <span className="text-sm">{creature.stats.attack}</span>
      </div>
      <div className="flex items-center gap-1">
        <Shield className="w-4 h-4" />
        <span className="text-sm">{creature.stats.defense}</span>
      </div>
    </div>
  </Card>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const opponentCreature = props.data?.entities?.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* HUD */}
      <Card className="rounded-none border-b">
        <div className="h-16 px-4 flex items-center justify-between">
          <span className="font-bold">{props.data.entities.player.display_name}</span>
          <span className="font-bold">Battle Scene</span>
        </div>
      </Card>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between px-8 py-4">
        <CreatureDisplay creature={playerCreature} isPlayer={true} />
        <CreatureDisplay creature={opponentCreature} isPlayer={false} />
      </div>

      {/* Action UI */}
      <Card className="rounded-none border-t">
        <ScrollArea className="h-[33vh]">
          <div className="p-4 grid grid-cols-2 gap-4">
            {playerCreature.collections.skills.map((skill) => (
              <Button
                key={skill.uid}
                variant={availableButtonSlugs.includes(skill.display_name.toLowerCase()) ? "default" : "secondary"}
                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                disabled={!availableButtonSlugs.includes(skill.display_name.toLowerCase())}
                className="h-auto py-4 flex flex-col items-start"
              >
                <span className="font-bold">{skill.display_name}</span>
                <Separator className="my-2" />
                <span className="text-sm text-left">{skill.description}</span>
              </Button>
            ))}
          </div>
        </ScrollArea>
      </Card>
    </div>
  );
}
