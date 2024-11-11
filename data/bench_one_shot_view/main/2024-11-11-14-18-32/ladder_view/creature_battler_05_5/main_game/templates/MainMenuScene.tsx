import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, Power } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

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
    entities: {
        active_creature?: Creature;
    };
    collections: {
        creatures: Creature[];
    };
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
    } = useCurrentButtons()

    if (!props.data) {
        return null;
    }

    return (
        <Card className="w-full h-full flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-800 to-slate-900 aspect-video border-0">
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data.display_name || "Main Menu"}
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-y-4 mb-16 w-64">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="w-full flex items-center justify-center gap-x-2 py-6 text-xl"
                        variant="default"
                    >
                        <Play className="w-6 h-6" />
                        <span>Play Game</span>
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="w-full flex items-center justify-center gap-x-2 py-6 text-xl"
                        variant="destructive"
                    >
                        <Power className="w-6 h-6" />
                        <span>Quit</span>
                    </Button>
                )}
            </div>
        </Card>
    )
}
