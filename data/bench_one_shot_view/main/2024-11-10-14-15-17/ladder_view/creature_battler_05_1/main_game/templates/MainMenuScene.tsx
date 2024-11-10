import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Skill {
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
    display_name: string;
    description: string;
}

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
        skills: Skill[];
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
    entities: {
        active_creature?: Creature;
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
    meta: Record<string, any>;
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

    return (
        <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-slate-900 to-slate-950 flex flex-col items-center justify-between p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data?.display_name || "CREATURE GAME"}
                </h1>
            </div>

            <div className="flex flex-col gap-4 mb-16">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        variant="default"
                        size="lg"
                        onClick={() => emitButtonClick('play')}
                        className="w-48 h-14 text-xl"
                    >
                        <Play className="mr-2 h-6 w-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        variant="destructive"
                        size="lg"
                        onClick={() => emitButtonClick('quit')}
                        className="w-48 h-14 text-xl"
                    >
                        <XCircle className="mr-2 h-6 w-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
