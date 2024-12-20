import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, X } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      display_name: string;
      description: string;
      collections: {
        creatures: Array<{
          uid: string;
          display_name: string;
          description: string;
          stats: {
            hp: number;
            max_hp: number;
          };
          collections: {
            skills: Array<{
              uid: string;
              display_name: string;
              description: string;
              stats: {
                damage?: number;
              };
            }>;
          };
        }>;
      };
    };
    bot: {
      uid: string;
      display_name: string;
      description: string;
      collections: {
        creatures: Array<{
          uid: string;
          display_name: string;
          description: string;
          stats: {
            hp: number;
            max_hp: number;
          };
          collections: {
            skills: Array<{
              uid: string;
              display_name: string;
              description: string;
              stats: {
                damage?: number;
              };
            }>;
          };
        }>;
      };
    };
    player_creature: {
      uid: string;
      display_name: string;
      description: string;
      stats: {
        hp: number;
        max_hp: number;
      };
      collections: {
        skills: Array<{
          uid: string;
          display_name: string;
          description: string;
          stats: {
            damage?: number;
          };
        }>;
      };
    };
    bot_creature: {
      uid: string;
      display_name: string;
      description: string;
      stats: {
        hp: number;
        max_hp: number;
      };
      collections: {
        skills: Array<{
          uid: string;
          display_name: string;
          description: string;
          stats: {
            damage?: number;
          };
        }>;
      };
    };
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Game HUD</h1>
      </nav>

      <div className="flex-grow flex items-center justify-between p-4">
        <Card className="w-1/3 bg-green-100 p-4">
          <h2 className="text-lg font-bold">{playerCreature?.display_name ?? 'Player Creature'}</h2>
          <p>HP: {playerCreature?.stats.hp ?? 0} / {playerCreature?.stats.max_hp ?? 0}</p>
          <div className="mt-2 flex items-center">
            <Shield className="mr-2" />
            <span>Player's Creature</span>
          </div>
        </Card>

        <Card className="w-1/3 bg-red-100 p-4">
          <h2 className="text-lg font-bold">{botCreature?.display_name ?? 'Opponent Creature'}</h2>
          <p>HP: {botCreature?.stats.hp ?? 0} / {botCreature?.stats.max_hp ?? 0}</p>
          <div className="mt-2 flex items-center">
            <Sword className="mr-2" />
            <span>Opponent's Creature</span>
          </div>
        </Card>
      </div>

      <div className="bg-gray-200 p-4">
        <Card className="bg-white p-4 mb-4">
          <p>Game description and status updates will appear here.</p>
        </Card>
        <div className="flex flex-wrap gap-2">
          {availableButtonSlugs.includes('quit') && (
            <Button onClick={() => emitButtonClick('quit')} variant="destructive">
              <X className="mr-2" />
              Quit
            </Button>
          )}
          {availableButtonSlugs.includes('tackle') && (
            <Button onClick={() => emitButtonClick('tackle')} variant="default">
              <Sword className="mr-2" />
              Tackle
            </Button>
          )}
          {availableButtonSlugs.includes('use-skill') && (
            <Button onClick={() => emitButtonClick('use-skill')} variant="secondary">
              Use Skill
            </Button>
          )}
          {playerCreature?.collections.skills.map((skill) => (
            <Button
              key={skill.uid}
              onClick={() => emitButtonClick(skill.uid)}
              variant="outline"
            >
              {skill.display_name}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
}
