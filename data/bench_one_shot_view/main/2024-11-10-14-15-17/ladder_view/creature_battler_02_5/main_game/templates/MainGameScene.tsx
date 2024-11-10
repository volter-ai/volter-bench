import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress"; 
import { Separator } from "@/components/ui/separator";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
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
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

function CreatureDisplay({ 
  creature, 
  isPlayer,
  uid
}: { 
  creature: Creature, 
  isPlayer: boolean,
  uid: string 
}) {
  const hpPercentage = (creature.stats.hp / creature.stats.max_hp) * 100;
  
  return (
    <Card className={`flex flex-col items-center p-4 ${isPlayer ? 'mr-auto' : 'ml-auto'}`}>
      <div className="text-lg font-bold mb-2">{creature.display_name}</div>
      <div className="w-48 h-48 bg-slate-200 rounded-lg flex items-center justify-center mb-2">
        {/* Creature sprite placeholder */}
        <span className="text-slate-600">{isPlayer ? "Player" : "Opponent"}</span>
      </div>
      
      <div className="w-full space-y-2">
        <div className="flex items-center gap-2">
          <Heart className="text-red-500 w-4 h-4" />
          <Progress value={hpPercentage} className="w-full" />
          <span className="text-sm">
            {creature.stats.hp}/{creature.stats.max_hp}
          </span>
        </div>
        
        <div className="flex justify-between">
          <div className="flex items-center gap-1">
            <Sword className="w-4 h-4" />
            <span className="text-sm">{creature.stats.attack}</span>
          </div>
          <div className="flex items-center gap-1">
            <Shield className="w-4 h-4" />
            <span className="text-sm">{creature.stats.defense}</span>
          </div>
        </div>
      </div>
    </Card>
  );
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const opponentCreature = props.data?.entities?.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return (
      <div className="w-full h-full aspect-video flex items-center justify-center">
        <Card className="p-4">Loading battle...</Card>
      </div>
    );
  }

  return (
    <div className="w-full h-full aspect-video flex flex-col">
      {/* HUD */}
      <Card className="rounded-none border-x-0 border-t-0">
        <div className="h-14 flex items-center justify-between px-4">
          <span className="font-semibold">{props.data.entities.player.display_name}</span>
          <span className="font-semibold">Battle Scene</span>
        </div>
      </Card>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between px-8 bg-slate-100">
        <CreatureDisplay 
          creature={playerCreature} 
          isPlayer={true}
          uid={playerCreature.uid} 
        />
        <CreatureDisplay 
          creature={opponentCreature} 
          isPlayer={false}
          uid={opponentCreature.uid}
        />
      </div>

      {/* Action UI */}
      <Card className="rounded-none border-x-0 border-b-0">
        <div className="h-[200px] p-4">
          <div className="grid grid-cols-2 gap-2">
            {playerCreature.collections.skills.map((skill) => {
              const isAvailable = availableButtonSlugs.includes(skill.display_name.toLowerCase());
              return (
                <Button
                  key={skill.uid}
                  variant={isAvailable ? "default" : "secondary"}
                  onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                  disabled={!isAvailable}
                  className="h-auto py-2"
                >
                  <div className="text-left">
                    <div className="font-semibold">{skill.display_name}</div>
                    <div className="text-sm opacity-90">{skill.description}</div>
                  </div>
                </Button>
              );
            })}
          </div>
        </div>
      </Card>
    </div>
  );
}
