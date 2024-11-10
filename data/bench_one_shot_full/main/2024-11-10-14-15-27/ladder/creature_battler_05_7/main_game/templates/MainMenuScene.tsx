import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

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
        skill_type: string;
        is_physical: boolean;
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
}

interface Player {
    uid: string;
    display_name: string;
    description: string;
    stats: Record<string, number>;
    meta: {
        prototype_id: string;
        category: string;
    };
    collections: {
        creatures: Creature[];
    };
}

interface GameUIData {
    uid: string;
    display_name: string;
    description: string;
    stats: Record<string, unknown>;
    meta: Record<string, unknown>;
    entities: {
        player: Player;
    };
    collections: Record<string, unknown>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data?.display_name || 'Main Menu'}
                </h1>
            </div>

            {/* Middle Spacer */}
            <div className="flex-1" />

            {/* Button Section */}
            <div className="flex-1 flex flex-col items-center justify-center gap-y-4">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        variant="default"
                        size="lg"
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center gap-x-2 px-8 py-6 text-xl"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        variant="destructive"
                        size="lg"
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center gap-x-2 px-8 py-6 text-xl"
                    >
                        <XCircle className="w-6 h-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
