import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface Creature {
    uid: string;
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        sp_attack: number;
        sp_defense: number;
        speed: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        creature_type: string;
    };
    collections: {
        skills: Array<{
            uid: string;
            stats: {
                base_damage: number;
            };
            meta: {
                prototype_id: string;
                category: string;
                skill_type: string;
                is_physical: boolean;
            };
        }>;
    };
    display_name: string;
    description: string;
}

interface Player {
    uid: string;
    stats: Record<string, number>;
    meta: {
        prototype_id: string;
        category: string;
    };
    collections: {
        creatures: Creature[];
    };
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
    };
    stats: Record<string, number>;
    meta: Record<string, string>;
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    if (!props.data) {
        return null;
    }

    const isButtonAvailable = (slug: string) => 
        availableButtonSlugs?.includes(slug) ?? false;

    return (
        <Card className="h-screen w-screen flex flex-col justify-between items-center 
                      bg-gradient-to-b from-slate-800 to-slate-900 p-8">
            
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-4xl md:text-6xl font-bold text-white 
                           tracking-wider uppercase">
                    {props.data.display_name || "Creature Battle Game"}
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-4 mb-16">
                {isButtonAvailable('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center justify-center gap-2 min-w-[200px]"
                        variant="default"
                        size="lg"
                    >
                        <Play className="w-5 h-5" />
                        <span>Play Game</span>
                    </Button>
                )}

                {isButtonAvailable('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center justify-center gap-2 min-w-[200px]"
                        variant="destructive"
                        size="lg"
                    >
                        <XCircle className="w-5 h-5" />
                        <span>Quit</span>
                    </Button>
                )}
            </div>
        </Card>
    );
}
