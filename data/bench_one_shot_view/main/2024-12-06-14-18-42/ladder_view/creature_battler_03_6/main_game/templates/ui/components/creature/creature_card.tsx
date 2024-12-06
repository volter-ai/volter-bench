import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as CardPrimitive,
  CardContent as CardContentPrimitive, 
  CardHeader as CardHeaderPrimitive, 
  CardTitle as CardTitlePrimitive 
} from "@/components/ui/card"
import { Progress as ProgressPrimitive } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface WithUid {
  uid: string
}

let Progress = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ProgressPrimitive> & WithUid>(
  ({ uid, ...props }, ref) => <ProgressPrimitive ref={ref} {...props} />
)

let Card = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardPrimitive> & WithUid>(
  ({ uid, ...props }, ref) => <CardPrimitive ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardContentPrimitive> & WithUid>(
  ({ uid, ...props }, ref) => <CardContentPrimitive ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardHeaderPrimitive> & WithUid>(
  ({ uid, ...props }, ref) => <CardHeaderPrimitive ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, React.ComponentProps<typeof CardTitlePrimitive> & WithUid>(
  ({ uid, ...props }, ref) => <CardTitlePrimitive ref={ref} {...props} />
)

Progress = withClickable(Progress)
Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="relative aspect-square w-full mb-4">
            <img
              src={imageUrl}
              alt={name}
              className="object-cover w-full h-full rounded-lg"
            />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{hp}/{maxHp}</span>
            </div>
            <Progress uid={`${uid}-progress`} value={(hp / maxHp) * 100} />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
