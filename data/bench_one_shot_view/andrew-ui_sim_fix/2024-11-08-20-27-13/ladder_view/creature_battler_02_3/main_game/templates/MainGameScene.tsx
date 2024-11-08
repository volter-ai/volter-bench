import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink
} from "@/components/ui/navigation-menu";

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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderCreatureStats = (creature: Creature | undefined, isPlayer: boolean) => {
    if (!creature) return null;
    
    return (
      <Card className={`p-4 ${isPlayer ? 'ml-8' : 'mr-8'}`}>
        <h2 className="text-xl font-bold mb-2">{creature.display_name}</h2>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Heart className="h-4 w-4 text-red-500" />
            <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
          </div>
          <div className="flex items-center gap-2">
            <Sword className="h-4 w-4 text-blue-500" />
            <span>{creature.stats.attack}</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-green-500" />
            <span>{creature.stats.defense}</span>
          </div>
        </div>
      </Card>
    );
  };

  return (
    <div className="w-full h-full flex flex-col">
      {/* HUD */}
      <NavigationMenu className="h-[10%]">
        <NavigationMenuList className="px-4 w-full justify-between">
          <NavigationMenuItem>
            <NavigationMenuLink>
              {props.data.entities.player?.display_name}
            </NavigationMenuLink>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <NavigationMenuLink>
              {props.data.entities.opponent?.display_name}
            </NavigationMenuLink>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>

      {/* Battlefield */}
      <div className="h-[60%] flex items-center justify-between">
        <div className="flex flex-col items-center">
          <span className="text-sm text-blue-500 mb-2">Player</span>
          {renderCreatureStats(props.data.entities.player_creature, true)}
        </div>
        
        <div className="flex flex-col items-center">
          <span className="text-sm text-red-500 mb-2">Opponent</span>
          {renderCreatureStats(props.data.entities.opponent_creature, false)}
        </div>
      </div>

      {/* UI Area */}
      <Card className="h-[30%] mt-auto">
        <div className="grid grid-cols-2 gap-4 p-4">
          {props.data.entities.player_creature?.collections.skills.map((skill) => (
            availableButtonSlugs.includes(skill.display_name.toLowerCase()) && (
              <Button
                key={skill.uid}
                variant="secondary"
                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
              >
                <div className="text-left">
                  <div className="font-bold">{skill.display_name}</div>
                  <div className="text-sm opacity-90">{skill.description}</div>
                </div>
              </Button>
            )
          ))}
        </div>
      </Card>
    </div>
  );
}
