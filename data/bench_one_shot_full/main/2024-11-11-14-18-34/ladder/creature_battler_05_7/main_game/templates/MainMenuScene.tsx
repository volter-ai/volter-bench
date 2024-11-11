import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface Skill {
    uid: string;
    __type: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        skill_type: string;
        is_physical: boolean;
    };
    display_name: string;
    description: string;
}

interface Creature {
    uid: string;
    __type: string;
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
        skills: Skill[];
    };
    display_name: string;
    description: string;
}

interface Player {
    uid: string;
    __type: string;
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
    __type: string;
    entities: {
        player: Player;
    };
    stats: Record<string, number>;
    meta: Record<string, string>;
    collections: Record<string, unknown>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    const isButtonAvailable = (slug: string) => 
        availableButtonSlugs?.includes(slug) ?? false;

    return (
        <div className="relative h-screen w-screen flex flex-col justify-between items-center 
                        bg-gradient-to-b from-slate-800 to-slate-900 p-8">
            <Card className="flex-1 w-full max-w-4xl flex flex-col items-center justify-between 
                           bg-opacity-50 backdrop-blur-sm">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-4xl md:text-6xl font-bold text-white 
                                 tracking-wider uppercase text-center">
                        {props.data?.display_name || "Creature Battle Game"}
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 mb-16 w-full max-w-md px-4">
                    {isButtonAvailable('play') && (
                        <Button
                            onClick={() => emitButtonClick('play')}
                            className="w-full h-12 text-lg"
                            variant="default"
                        >
                            <Play className="mr-2 h-5 w-5" />
                            Play Game
                        </Button>
                    )}

                    {isButtonAvailable('quit') && (
                        <Button
                            onClick={() => emitButtonClick('quit')}
                            className="w-full h-12 text-lg"
                            variant="destructive"
                        >
                            <XCircle className="mr-2 h-5 w-5" />
                            Quit
                        </Button>
                    )}
                </div>
            </Card>
        </div>
    );
}
