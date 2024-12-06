import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import { Progress as ShadcnProgress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

// Create wrapped versions with uid
let Progress = withClickable(
  React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ShadcnProgress> & { uid: string }>(
    ({ uid, ...props }, ref) => <ShadcnProgress ref={ref} {...props} />
  )
)

let Card = withClickable(
  React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ShadcnCard> & { uid: string }>(
    ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
  )
)

let CardContent = withClickable(
  React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ShadcnCardContent> & { uid: string }>(
    ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
  )
)

let CardHeader = withClickable(
  React.forwardRef<HTMLDivElement, React.ComponentProps<typeof ShadcnCardHeader> & { uid: string }>(
    ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
  )
)

let CardTitle = withClickable(
  React.forwardRef<HTMLHeadingElement, React.ComponentProps<typeof ShadcnCardTitle> & { uid: string }>(
    ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
  )
)

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
